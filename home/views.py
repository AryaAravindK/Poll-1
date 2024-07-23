from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, MCQ, Descriptive, UserInfo, Response
from .forms import UserInfoForm

def index(request):
    polls = Poll.objects.all()
    responses = Response.objects.order_by('-submit_time','score')

    return render(request, 'polls/index.html', {'polls': polls, 'responses':responses})

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    mcqs = MCQ.objects.filter(poll=poll)
    descriptions = Descriptive.objects.filter(poll=poll)

    if request.method == 'POST':
        if 'name' in request.POST and 'phone_number' in request.POST:
            # User information submission
            user_form = UserInfoForm(request.POST)
            if user_form.is_valid():
                user_info = user_form.save()
                request.session['user_info_id'] = user_info.id
                return redirect('poll_detail', poll_id=poll.id)
        else:
            # Poll submission
            user_info_id = request.session.get('user_info_id')
            if not user_info_id:
                return redirect('poll_detail', poll_id=poll.id)

            user_info = UserInfo.objects.get(pk=user_info_id)
            total_score = 0
            total_mcqs = mcqs.count() + descriptions.count()

            for mcq in mcqs:
                choice = request.POST.get(f'choice_{mcq.id}')
                if choice:
                    selected_option = getattr(mcq, f'option{choice.upper()}')
                    if selected_option == mcq.correct_answer:
                        total_score += 1
            for desc in descriptions:
                user_answer = request.POST.get(f'answer_{desc.id}')
                if user_answer:
                    is_correct = user_answer.strip().lower() == desc.answer.strip().lower()
                    if is_correct:
                        total_score += 1

            # Calculate the percentage score
            percentage_score = (total_score / total_mcqs * 100) if total_mcqs else 0

            # Save the response
            Response.objects.create(
                user_info=user_info,
                poll=poll,
                score=percentage_score,
                submit_time=timezone.now()
            )

            # Redirect to results
            return redirect('poll_results', poll_id=poll.id)
    else:
        user_info_id = request.session.get('user_info_id')
        user_form = UserInfoForm() if not user_info_id else None
        return render(request, 'polls/poll_detail.html', {
            'poll': poll,
            'mcqs': mcqs,
            'descriptions': descriptions,
            'user_form': user_form,
        })

def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    responses = Response.objects.filter(poll=poll)
    return render(request, 'polls/poll_results.html', {'poll': poll, 'responses': responses})
