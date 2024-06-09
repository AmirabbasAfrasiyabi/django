const PersianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
const ArabicDigits  = ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"]
const EnglishDigits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
  
function ConvertToEnglish(Tagname){
  $(Tagname).on('input', function(){
    var str = $(this).val();
    for (let i =0; i < 10; i++){
      var rep = str.replace(PersianDigits[i], EnglishDigits[i]);
      var rep = rep.replace(ArabicDigits[i], EnglishDigits[i]);
      var str = rep;
    }
    $(this).val(rep.replace(/[^0-9\.]+/g, ""));
  });
}

function ConvertToPersian(Tagname){
  $(Tagname).on('input', function(){
    var str = $(this).val();
    for (let i =0; i < 10; i++){
      var rep = str.replace(EnglishDigits[i], PersianDigits[i]);
      var rep = rep.replace(ArabicDigits[i], PersianDigits[i]);
      var str = rep;
    }
    $(this).val(rep.replace(/[^۰-۹\.]+/g, ""));
  });
}