  /*
  This const "commentEntries" are used to divide the comments by different
  backgroundcolors. Comments with even entry has a backgroundcolor of #F0FBFF
  and uneven entries has backgroundcolor #FFFFFF. 

  It´s better to use entrynumber than Ids to decide backgroundcolors, because
  if a user deletes for example comment no.2 the first entries (Id no.1 and 3 will
  both have #FFFFFF as backgroundcolor. This isn´t a good UX, instead this const
  uses entrynumber. So if a user wants to delete Id no.2 that doesn´t affect 
  the backgroundcolors that divides the comments.
  */
  const commentEntries = document.getElementsByClassName("comment-entry");
  for (let i = 0; i < commentEntries.length; i++) {
    if (i % 2 === 0) {
      commentEntries[i].style.backgroundColor = "#F0FBFF";
    } else {
      commentEntries[i].style.backgroundColor = "#FFFFFF";
    }
  }


  const editButtons = document.getElementsByClassName("btn-edit");
  const deleteButtons = document.getElementsByClassName("btn-delete");
  const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  const deleteForm = document.getElementById("deleteForm");
  const deleteCommentContent = document.getElementById("deleteCommentContent");
  const commentText = document.getElementById("id_content");
  const submitButton = document.getElementById("submitButton");
  const commentForm = document.getElementById("commentForm");


  /*
  When a user wants to edit their own comment by pressing the edit button, this specific
  comment will appear in the commenting form and the submit button will change to 
  "update".
  */
  for (let button of editButtons) {
    button.addEventListener("click", (e) => {
      let commentId = e.target.getAttribute("data-comment_id");
      let commentContent = document.getElementById(`comment${commentId}`).innerText.trim();
      if (commentText) {
        commentText.value = commentContent;
      } else {
        console.error("Element with id 'id_content' not found");
      }
      if (submitButton) {
        submitButton.innerText = "Update";
      }
      if (commentForm) {
        commentForm.setAttribute("action", `/edit_comment/${commentId}/`);
      }
    });
  }


  /* 
  When pressing "delete" on a comment a modal will be shown. 
  In that modal this specific comment will be shown and asking 
  the user if they are sure to delete their comment or not.
  */
   for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      let commentId = e.target.getAttribute("data-comment_id");
      let commentContent = e.target.getAttribute("data-comment_content");
      if (deleteCommentContent) {
        deleteCommentContent.innerText = commentContent;
      }
      if (deleteForm) {
        deleteForm.setAttribute("action", `/delete_comment/${commentId}/`);
      }
      deleteModal.show();
    });
  }

