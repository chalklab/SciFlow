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
        if (nss.includes(':' + meta[1].toLowerCase() + ':')) {
            alert('An ontology with this namespace is already in use');
        } else {
            $('#name').val(meta[0]);
            $('#alias').val(meta[1]);
            $('#path').val(meta[2]);
            $('#homepage').val(meta[3]);
        }
        return false;
    });

    // for ols ont list in template ontterms/add.html
    $('#olsont').on('change', function() {
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
                    let btn = '<input class="btn btn-sm btn-success terms m-1" data-alias="' + ontid + '" data-code="' + term[3] + '" data-defn="' + term[2] + '" type="button" title="' + term[1] + '" value="' + term[1] + '">'
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

    // populate onto term from ontology button on
    $('#ontterms').on('click','.terms', function() {
        // set event to fire on parent of dynamically added dom element ('.term')
        let term = $(this);
        let title = term.val();
        let nsid = term.attr('data-alias');
        let code = term.attr('data-code');
        let defn = term.attr('data-defn');
        $('#title').val(title);
        $('#definition').val(defn);
        $('#code').val(code);
        $('#nsid').val(nsid);
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
    $(".updcwk").on('change', function () {
        let input = $(this);
        let field = input.attr('id');
        let form = input.closest('form');
        let cwkid = form.attr('cwkid')
        let cxtid = form.attr('cxtid')
        let value = input.val();
        // if dbid is empty create new entry in crosswalks table
        let url = 'http://127.0.0.1:8000/xwalks/add/';
        $.ajax({
            type: 'POST',
            dataType: "json",
            context: document.body,
            url: url,
            data: {cwkid: cwkid, cxtid: cxtid, field: field, value: value },
            success: function (data) {
                // note ontterm title and url put in temp field (title|url)
                let html = '<b>' + data.table + ':' + data.field + ' -> </b>';
                if(data.newname) {
                    html += ' ' + data.newname;
                } else {
                    html += ' ' + data.field;
                }
                html += ' (' + data.datatype + ')';
                if(data.temp) {
                    let temp = data.temp.split('|');
                    html += ' means <em>' + temp[0] + '</em> [' + temp[1] + ']';
                }
                if(!cwkid) {
                    // set the crosswalk id if it was not set (new entry)
                    $('#modalform').attr("cwkid",data.id);
                    // add the new entry to the page
                    let newitem = '<div class="col-11 pr-0">';
                    newitem += '<a id="cwk' + data.id + '" class="editcwk list-group-item items py-1" cwkid="' + data.id + '" data-toggle="modal" data-target="#cwkmodal" style="cursor: pointer;">' + html + '</a>';
                    newitem += '</div><div class="col-1 pl-0">';
                    newitem += '<button class="btn btn-sm btn-danger delcwk col-12" cwkid="' + data.id + '" title="Delete">X</button>'
                    newitem += '</div>';
                    $("#cwks").append(newitem);
                } else {
                    $('#cwk' + cwkid).html(html);
                }
                return false;
            },
            error: function () {
                alert("Error");
                return false;
            }
        });
        return false;
    });

    // remove a crosswalk entry
    $(".delcwk").on('click', function () {
        let cwk = $(this);
        let cwkid = cwk.attr('cwkid');
        $.post('/xwalks/delete/', {cwkid: cwkid})
            .done(function ( data ) {
                // hide dom elements
                if(data['response']==='success') {
                    $(".editcwk[cwkid='" + cwkid + "']").hide();
                    $(".delcwk[cwkid='" + cwkid + "']").hide();
                    alert("Crosswalk deleted :)");
                } else {
                    alert("Deletion error :(");
                }
            });
        return false;
    });

    // search and show/hide terms in card
    $("#listsrc").on('keyup',function(){
        let val=$(this).val().toLowerCase().trim();
        let items=$('.items');
        let terms=$('.terms');
        let delbtns=$('.delcwk');
        items.show(); // for html elements that have content inside the element
        terms.show(); // for buttons (with attr 'value')
        delbtns.show(); // for crosswalks to also hide delete buttons along with <a> links
        console.log(val);
        if(val!=='') {
            terms.not('[value*="' + val + '"]').hide();
            let nomatch = items.not(':contains(' + val + ')')
            nomatch.each(function (i, el) {
                let item=$(el);
                $(".delcwk[cwkid='" + item.attr('cwkid') + "']").hide();
            });
            nomatch.hide();
        }
    });

    // create context JSON-LD file
    $("#createctx").on('click', function () {
        let id = $("#createctx").attr('dbid');
        $.get('/contexts/write/' + id).done(function() { alert( "Context file saved :)" ); });
        return false;
    });

    // add a new crosswalk entry
    $("#addcwk").on('click', function () {
        // clear form
        let form = $('#modalform');
        form[0].reset();
        form.attr('cwkid','');
        form.attr('cxtid','');
        // process
        let btn = $(this);
        let cxtid = btn.attr('cxtid');
        form.attr("cxtid",cxtid);
    });

    // edit a crosswalk entry
    $(".editcwk").on('click', function () {
        let cwk = $(this);
        let cwkid = cwk.attr('cwkid');
        $.get('/xwalks/read/' + cwkid, function( data ) {
            $('#modalform').attr("dbid",cwkid);
            $('#table').val(data.table).attr('old',data.table);
            $('#field').val(data.field).attr('old',data.field);
            $('#ontterm_id').val(data.ontterm);
            $('#sdsection').val(data.sdsection);
            $('#sdsubsection').val(data.sdsubsection).attr('old',data.sdsubsection);
            $('#sdsubsubsection').val(data.sdsubsubsection).attr('old',data.sdsubsubsection);
            $('#newname').val(data.newname).attr('old',data.newname);
            $('#category').val(data.category).attr('old',data.category);
            $('#datatype').val(data.datatype);
            return false;
        });
    });

    // focus modal to first input field on open
    $('#cwkmodal').on('shown.bs.modal', function () {
        $('#table').trigger('focus')
    });

});