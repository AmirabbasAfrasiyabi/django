function LimitFileUploadFormatvideo (vid){
                        var x = $(vid).val();
                        var ext_vid = x.match(/\.([^\.]+)$/)[1];
                        switch (ext_vid) {
                        case 'mp4'  :
                            videovalidation = "valid";
                            break;
                        default:
                            $(vid).val('');
                            videovalidation = "invalid";
                        }
                    
            return videovalidation;
}