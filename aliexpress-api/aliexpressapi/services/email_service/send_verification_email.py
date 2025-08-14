class SendVerificationEmail(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.is_verified:
            return Response(
                {"status": "email-already-verified"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Generate email verification token
        uid = urlsafe_base64_encode(user.pk.encode("utf-8"))
        token = default_token_generator.make_token(user)

        # Generate verification link
        verification_link = f"http://{get_current_site(request).domain}{
            reverse('email_verification', kwargs={'uidb64': uid, 'token': token})
        }"

        # Send verification email
        send_mail(
            "Email Verification",
            f"Please verify your email using this link: {verification_link}",
            "from@example.com",
            [user.email],
            fail_silently=False,
        )

        return Response({"status": "verification-link-sent"}, status=status.HTTP_200_OK)
