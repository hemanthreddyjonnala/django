from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            # try:
            #     send_mail(subject, message, from_email, ['jonnalapycreations@gmail.com'])
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
            # return redirect('success')

            message = Mail(
                from_email=from_email,
                to_emails='jonnalapycreations@gmail.com',
                subject=subject,
                html_content=message)
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                print(sg)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                return HttpResponse(e)
            return redirect('success')
    return render(request, "contact/email.html", {'form': form})


def successView(request):
    return render(request, "contact/success.html")