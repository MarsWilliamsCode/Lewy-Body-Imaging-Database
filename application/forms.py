from django import forms
from .models import Image
import credentials
class ImageAdminForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_id', 'scan_id', 'image_type', 'image_file', 'image_url']

    def save(self, commit=True):
        # Get the image file from the form
        image_file = self.cleaned_data.get('image_file')
        scan_id = self.cleaned_data.get('scan_id')
        image_id = self.cleaned_data.get('image_id')

        if image_file:
            # Define the object key for S3
            object_key = f"{image_file}"

            # Upload the image to S3 and get the public URL
            s3_url = f"https://{credentials.AWS_STORAGE_BUCKET_NAME}.s3.{credentials.AWS_S3_REGION_NAME}.amazonaws.com/{object_key}"

            # Set the public URL in the instance before saving
            self.instance.image_url = s3_url

        return super().save(commit=commit)