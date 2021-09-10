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

    $('.olsont').on('click', function() {
        // for ols ont list in template nspaces/add.html
        let ont = $(this);
        let meta = ont.attr('data-ont').split("*");
        let nss = $('#aliases').html();
        if (nss.includes(meta[1])) {
            alert('An ontology with this namespace is already in use');
        } else {
            $('#name').val(meta[0]);
            $('#alias').val(meta[1]);
            $('#path').val(meta[2]);
            $('#homepage').val(meta[3]);
        }
        return false;
    });

    $('#olsont').on('change', function() {
        // for ols ont list in template ontterms/add.html
        let ontid = $('#olsont option:selected').val();
        $.ajax({
            type: 'POST',
            dataType: "json",
            context: document.body,
            url: 'http://127.0.0.1:8000/ontterms/js/' + ontid,
            success: function (data) {
                let terms = data['ontterms'];
                let cnt = terms.length;
                let div = $("#ontterms");
                div.html('');
                for(let i = 0; i<cnt; i++) {
                    let term = terms[i];
                    let btn = '<input class="btn btn-sm btn-success term m-1" data-alias="' + ontid + '" data-code="' + term[3] + '" data-defn="' + term[2] + '" type="button" title="' + term[1] + '" value="' + term[1] + '">'
                    div.append(btn);
                }
                return false;
                },
            error: function () {
                alert("Error");
                return false;
            }
        });
    });

    $('#ontterms').on('click','.term', function() {
        // set event to fire on parent of dynamically added dom element ('.term')
        let term = $(this);
        let title = term.val();
        let nsid = term.attr('data-alias');
        let code = term.attr('data-code');
        let defn = term.attr('data-defn');
        $('#title').val(title);
        $('#definition').val(defn);
        $('#code').val(code);
        $('#ns_id').val(nsid);
        return false;
    });

    // show a new crosswalk entry...
    $("#showcwk").on('click', function () {
        let table=$(this).attr('data-table');
        let type=table.substring(0,table.length-1);
        let nnum=$("." + type).length;
        let clone=$("#" + type + "0").clone(true,true);
        clone.attr('id',type + nnum);
        clone.attr('data-nnum',nnum);
        clone.removeClass('invisible');
        clone.removeClass('collapse');
        clone.find("#index" + nnum).text(nnum); // table field
        clone.find("#tbl0").attr('id','tbl' + nnum); // table field
        clone.find("#fld0").attr('id','fld' + nnum); // field field
        clone.find("#trm0").attr('id','trm' + nnum); // ont term field
        clone.find("#sec0").attr('id','sec' + nnum); // section field
        clone.find("#typ0").attr('id','typ' + nnum); // aspect/facet type field
        clone.find("#cat0").attr('id','cat' + nnum); // category field
        clone.find("#dtp0").attr('id','dtp' + nnum); // datatype field
        clone.insertAfter("div." + type + ":last");
    });

    // add/update a new crosswalk entry...
    $(".updcwk").on('blur change', function () {
        let ipt = $(this).parent();
        let val = ipt.val();
        if(val === ipt.attr('data-old')) {
            return false;
        }
        alert(val);
        return false;
        let cwk = ipt.parent();
        let nnum = cwk.attr('data-nnum')
        let dbid = cwk.attr('data-dbid');
        let tbl = cwk.find("#tbl" + nnum).val();
        let fld = cwk.find("#fld" + nnum).val();
        let trm = cwk.find("#trm" + nnum).val();
        let sec = cwk.find("#sec" + nnum).val();
        let typ = cwk.find("#typ" + nnum).val();
        let cat = cwk.find("#cat" + nnum).val();
        let dtp = cwk.find("#dtp" + nnum).val();
        // if dbid is empty create new entry in crosswalks table
        let url = 'http://127.0.0.1:8000/xwalks/jscwkadd/' + dbid;
        $.ajax({
            type: 'POST',
            dataType: "json",
            context: document.body,
            url: url,
            data: {table: tbl, field: fld, term: trm, section: sec, sdtype: typ, category: cat, datatype: dtp },
            success: function (data) {
                let terms = data['ontterms'];
                let cnt = terms.length;
                let div = $("#ontterms");
                div.html('');
                for(let i = 0; i<cnt; i++) {
                    let term = terms[i];
                    let btn = '<input class="btn btn-sm btn-success term m-1" data-alias="' + ontid + '" data-code="' + term[3] + '" data-defn="' + term[2] + '" type="button" title="' + term[1] + '" value="' + term[1] + '">'
                    div.append(btn);
                }
                return false;
                },
            error: function () {
                alert("Error");
                return false;
            }
        }).done(function() {
            ipt.attr('data-old',val);
        });
        return false;
    });

    // remove a crosswalk entry
    $(".rmcwk").on('click', function () {
        let cwk = $(this).parent().parent();
        let nnum = cwk.attr('data-nnum');
        let tbl = cwk.find("#tbl" + nnum).val();
        let fld = cwk.find("#fld" + nnum).val();
        let trm = cwk.find("#trm" + nnum + " option:checked").val();
        let sec = cwk.find("#sec" + nnum + " option:checked").val();
        let typ = cwk.find("#typ" + nnum).val();
        let cat = cwk.find("#cat" + nnum).val();
        let dtp = cwk.find("#dtp" + nnum + " option:checked").val();
        alert(tbl + ':' + fld + ':' + trm + ':' + sec + ':' + typ + ':' + cat + ':' + dtp);
        return false;
    });

    // search and show/hide terms in card
    $("#cwksrc").on('keyup',function(){
        let val=$(this).val().toLowerCase().trim();
        let cwks=$('#cwks li');
        cwks.show();
        if(val!=='') {
            cwks.not('[title*="' + val + '"]').hide();
        }
    });

});