/* Sends a request to the owner's inbox through FormSubmit. The ONLY file with the
   endpoint. Resolves only when FormSubmit CONFIRMS the send: a 200 with
   success:"false" (e.g. not activated yet) also rejects. FormSubmit can be slow or
   not answer at all: after 20 s this rejects with error.late = the request still in
   flight, in case it is confirmed later. */
(function () {
  "use strict";
  var ENDPOINT = "https://formsubmit.co/ajax/jesusnodarse1823@gmail.com";
  var TIMEOUT = 20000;

  window.mpSubmit = function (payload) {
    var request = fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) { if (!r.ok) throw new Error("http"); return r.json(); })
      .then(function (d) {
        if (d && (d.success === "true" || d.success === true)) return d;
        throw new Error("pending");
      });
    return new Promise(function (resolve, reject) {
      var timer = setTimeout(function () {
        var e = new Error("timeout");
        e.late = request;
        reject(e);
      }, TIMEOUT);
      request.then(
        function (d) { clearTimeout(timer); resolve(d); },
        function (e) { clearTimeout(timer); reject(e); }
      );
    });
  };
})();
