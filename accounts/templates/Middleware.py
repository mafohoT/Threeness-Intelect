class AuthRequredMiddleware(object):
    def process_request(self,request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('Just.html'))
