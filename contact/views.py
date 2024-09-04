from .forms import ContactForm
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage


def contact(request):
    """
    Handle the contact form submission and send an email.

    This view processes the contact form submission.
    If the form is submitted and valid, it sends an email with the form details
    to a specified reciever and redirects the user to a success page.
    If the form is invalid, it renders the contact form page again.

    Args:
        request (HttpRequest): The request object used to generate this view.

    Returns:
        HttpResponse: The contact form page rendered with an empty form.
        HttpResponseRedirect: Redirect to the success page
                              after a successful form submission.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            EmailMessage(
                'Contact Form Submission from {}'.format(name),
                message,
                'form-response@racketclub.com',
                ['professoro88@gmail.com'],
                [],
                reply_to=[email]
            ).send()
            return redirect('success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def success(request):
    """
    Render the success page when the contact form submission is valid.

    This view renders a simple success page to inform the user that their
    contact form submission was successful.

    Args:
        request (HttpRequest): The request object used to generate this view.

    Returns:
        HttpResponse: The rendered success page.
    """
    return render(request, 'success.html')
