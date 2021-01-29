!(function () {
    var e = document.getElementById("cbp-vm"),
        t = Array.prototype.slice.call(e.querySelectorAll("div.cbp-vm-options > a"));
    t.forEach(function (c, a) {
        c.addEventListener(
            "click",
            function (c) {
                var a;
                c.preventDefault(),
                    (a = this),
                    t.forEach(function (t) {
                        classie.remove(e, t.getAttribute("data-view")), classie.remove(t, "cbp-vm-selected");
                    }),
                    classie.add(e, a.getAttribute("data-view")),
                    classie.add(a, "cbp-vm-selected");
            },
            !1
        );
    });
})();
