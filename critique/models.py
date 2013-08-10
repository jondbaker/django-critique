from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Critique(models.Model):
    created = models.DateTimeField(_("created"), default=now, editable=False)
    email = models.EmailField(_("email"))
    message = models.TextField(_("message"))
    url = models.URLField(_("url"))
    user_agent = models.CharField(_("user agent"), max_length=256)

    class Meta:
        ordering = ["-created"]

    def __unicode__(self):
        return u"{0} {1}".format(self.url, self.email)
