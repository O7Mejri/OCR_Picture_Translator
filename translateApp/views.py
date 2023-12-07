from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import json
import numpy as np
import os
import base64


from .functions import run, images_to_pdf, image_to_pdf
    
@csrf_exempt
def translate(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            img_url = data.get('url', '')
            dest_lang = data.get('lang', 'en')
            output, type = run(img_url, dest_lang)
            print("type :",type)
            if type == 'image':
                ## This is for when you want to send back an image instead of pdf
                ## Convert the modified image to base64

                # print(output)
                # _, img_buffer = cv2.imencode('.jpg', output)
                # img_base64 = base64.b64encode(img_buffer).decode('utf-8')
                # print(img_base64)
                # return JsonResponse({'status': 'success', 'images': img_base64})
                # _, img_buffer = cv2.imencode('.jpg', output)
                # img_bytes = img_buffer.tobytes()

                pdf_img_path = image_to_pdf("data/modified_image.jpg", "data/res_img_pdf.pdf")
                try:
                    with open(pdf_img_path, 'rb') as pdf_file:
                        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                        response['Content-Disposition'] = 'inline; filename="result.pdf"'
                        return response
                except FileNotFoundError:
                    return JsonResponse({'status': 'error', 'message': 'PDF file not found'})
                finally:
                    # Optionally, you can remove the created PDF file after serving it
                    os.remove(pdf_img_path)

            else:
                try:
                    with open(output, 'rb') as pdf_file:
                        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                        response['Content-Disposition'] = 'inline; filename="result.pdf"'
                        return response
                except FileNotFoundError:
                    return JsonResponse({'status': 'error', 'message': 'PDF file not found'})
                finally:
                    # Optionally, you can remove the created PDF file after serving it
                    os.remove(output)

        except Exception as e:
            print("type :",e)
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        print("type :",e)
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})