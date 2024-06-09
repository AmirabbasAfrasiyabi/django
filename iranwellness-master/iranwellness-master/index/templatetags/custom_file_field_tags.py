from django import template
import os

register = template.Library()

@register.filter
def get_file_extension(file):
  file_extension = os.path.splitext(file.name)[1].lower()
  archive_extensions = [".zip",".rar"]
  picture_extensions = [".png",".jpg",".jpeg"]
  if ( file_extension == ".pdf" ):
    return "pdf"
  if ( file_extension in archive_extensions ):
    return "archive"
  if (file_extension in picture_extensions ):
    return "picture"
  return "other"

@register.filter
def get_file_name(file):
  base = os.path.basename(file.name)
  file_name = os.path.splitext(base)[0] if len(os.path.splitext(base)[0]) <=20 else os.path.splitext(base)[0][0:17]+'...'
  return file_name