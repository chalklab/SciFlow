$(document).ready(function() {
    $('#alias').on('blur', function() {
        // for form in template nspaces/add.html
        let input = $('#alias');
        let nss = $('#aliases').html();
        let ns = input.val();
        if (nss.includes(ns)) {
            input.val('');
            alert('Alias already in use');
        }
        return false;
    });
});