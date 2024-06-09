function LimitFileUploadFormatImage (pic){
                        var x = $(pic).val();
                        var ext_pic = x.match(/\.([^\.]+)$/)[1];
                        switch (ext_pic) {
                        case 'jpg'  :
                        case 'jpeg' :
                        case 'JPEG' :
                        case 'pjpeg':
                        case 'bmp'  :
                        case 'png'  :
                        case 'PNG'  :
                        case 'tif'  :
                        case 'tiff' :
                        case 'jfif' :
                        case 'TIFF' :
                        case 'svg'  :
                        case 'svgz' :
                        case 'xbm'  :
                        case 'pjp'  :
                        case 'webp' :
                        case 'ico'  :
                        case 'gif'  :
                            Imagevalidation = "valid";
                            break;
                        default:
                            $(pic).val('');
                            Imagevalidation = "invalid";
                        }
                    
            return Imagevalidation;
}