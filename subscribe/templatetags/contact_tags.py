from django import template
from subscribe.forms import ContactForm

register = template.Library()

@register.inclusion_tag("contact/tags/email_form.html")
def contact_form():
    return {"contact_form": ContactForm()}
