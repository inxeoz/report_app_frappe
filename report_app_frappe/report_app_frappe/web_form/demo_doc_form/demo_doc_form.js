

frappe.ready(function () {
  const webForm = frappe.web_form;
  const webFormName = webForm?.name;

  // Extract docname from URL
  const docname = (() => {
    const parts = window.location.pathname.split('/').filter(Boolean);
    return parts[1] || null;
  })();

  // Hide default buttons
  ['.discard-btn', '.submit-btn'].forEach(selector => {
    const btn = document.querySelector(selector);
    if (btn) btn.style.display = 'none';
  });

  // Find target container
  const target = document.querySelector('.web-form-footer') || document.body;

  // Create "Edit" button
  const editBtn = document.createElement('button');
  editBtn.innerText = "Edit";
  editBtn.className = "btn btn-primary";
  editBtn.style.margin = "20px 10px 0 0";
  editBtn.onclick = () => {
    if (webFormName && docname) {
      window.location.href = `/${webFormName}/${docname}/edit`;
    } else {
      frappe.msgprint("Missing web form name or docname.");
    }
  };

  // Create "Submit" button
  const submitBtn = document.createElement('button');
  submitBtn.innerText = "Submit";
  submitBtn.className = "btn btn-success";
  submitBtn.style.marginTop = "20px";
  submitBtn.onclick = () => {
    if (webForm?.save) {
      webForm.save(); // actually submits the form
    } else {
      frappe.msgprint("Web form not ready to submit.");
    }
  };

  // Append buttons
  target.appendChild(editBtn);
  target.appendChild(submitBtn);
});
