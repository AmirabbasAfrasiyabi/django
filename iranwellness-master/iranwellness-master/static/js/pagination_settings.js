$(document).ready(function() {
    
    let has_previous_dots_pagination = false;
    let has_next_dots_pagination = false;
    
    const min_number_of_prev_next_pages_pagination = 2;
    const current_page_num = $('.active').index('.page-num');

    $(".page-num").not(":first,:last").each((index, item)=>{
        let base_index = index + 1;
        if ( base_index < current_page_num-min_number_of_prev_next_pages_pagination ){
            $(item).addClass('d-none');
            has_previous_dots_pagination=true;
        } else if ( base_index > current_page_num+min_number_of_prev_next_pages_pagination ) {
            $(item).addClass('d-none');
            has_next_dots_pagination=true;
        }
    });
    
    const dots = "<li class='page-item disabled'><span class='page-link'>...</span></li>";
    
    if(has_previous_dots_pagination){
        $('.page-num:first').after(dots);
    };

    if(has_next_dots_pagination){
        $('.page-num:last').before(dots);
    };
});