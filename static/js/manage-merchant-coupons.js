function checkAll(ckAll) {
	var sons = $($(ckAll).closest(".table").get(0)).find("input:checkbox[name='checkbox_coupon_id']");
	$.each(sons, function (index, checkbox) {
		if (!$(checkbox).attr("disabled")) {
		    $(checkbox).prop("checked", ckAll.checked);
		}
	})}

function delete_coupon_by_ids() {
    var ckboxs = $($(".table tbody").get(0)).find("input:checkbox[name='checkbox_coupon_id']:checked");
    if (!ckboxs.length) {
        alert("请勾选要停用的优惠券");
        return false;
     }
     var ids = "";
     for (var i = 0; i < ckboxs.length; i++) {
        ids += $(ckboxs[i]).val() + ",";
     }
     ids = ids.substring(0, ids.length - 1);
     var key = $("#key").val()
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     post_data = {"ids":ids, "key":key, "csrfmiddlewaretoken":csrf}
     $.post("/delete_coupon_by_ids/", post_data, function(result){
        window.location.reload()
     })
}