$(function () {

    function total() {
        let t = 0;
        $("input[type=checkbox]:checked").each(function () {
            t += parseInt($(this).data("price"));
        });
        $("#total").text(t);
        return t;
    }

    $("input[type=checkbox]").change(total);

    $("#pay").click(function () {
        let services = [];
        $("input[type=checkbox]:checked").each(function () {
            services.push($(this).val());
        });

        $.ajax({
            url: "/process_payment",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                patient_name: $("#patient_name").val(),
                patient_id: $("#patient_id").val(),
                visit_id: $("#visit_id").val(),
                services: services,
                amount: total(),
                payment_method: $("#payment_method").val(),
                remarks: $("#remarks").val()
            }),
            success: function (res) {
                $("#result").text("Payment successful. Txn ID: " + res.transaction_id);
            }
        });
    });
});
