$(".categoryRootMobile").hide(),
    $(".priceChecbkox").click(function () {
        $(".priceChecbkox").prop("checked", !1), $(this).prop("checked", !0);
        let e = $(this).attr("price");
        $("#totalPriceDelivery").text(e);
        let c = $("#totalPriceCartItems").attr("price_cart"),
        eStr = e.toString();
        cStr = c.toString();
        if (cStr.includes(",")){
            t = Math.round(100 * (parseFloat(eStr.replace(/\,/g, ".")) + parseFloat(cStr.replace(/\,/g, ".")))) / 100;
            $("#totalPriceAll").text(t);
        }else{
            t = Math.round(100 * (parseFloat(eStr)) + parseFloat(cStr)) / 100;
            $("#totalPriceAll").text(t);
        }
        
    }),
    $(".checkboxInvoice").change(function () {
        $(this).prop("checked") ? $(".invoiceFromWrapper").fadeIn("slow") : $(".invoiceFromWrapper").fadeOut("slow");
    });
