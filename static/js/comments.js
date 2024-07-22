console.log("comments.js is loaded");

const editButtons = document.getElementsByClassName("btn-edit");
const commentText = document.getElementById("id_content"); 
const commentForm = document.getElementById("commentForm");
const submitButton = document.getElementById("submitButton");

document.addEventListener('DOMContentLoaded', function() {
  const deleteButtons = document.getElementsByClassName("btn-delete");
  const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
  const deleteForm = document.getElementById("deleteForm");
  const deleteCommentContent = document.getElementById("deleteCommentContent");
  const deleteCommentId = document.getElementById("deleteCommentId");

  for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      let commentId = e.target.getAttribute("data-comment_id");
      let commentContent = e.target.getAttribute("data-comment_content");
      let articleSlug = e.target.getAttribute("data-article_slug");

      // Set form action to the delete URL
      deleteForm.action = `/${articleSlug}/delete_comment/${commentId}/`;

      // Display the comment content in the modal
      deleteCommentContent.textContent = commentContent;
      deleteModal.show();
    });
  }
});

console.log(editButtons, commentText, commentForm, submitButton, deleteModal, deleteButtons, deleteConfirm);

if (commentText === null) {
    console.error("Element with ID 'id_body' not found");
} else {
    /**
     * Initializes edit functionality for the provided edit buttons.
     * 
     * For each button in the `editButtons` collection:
     * - Retrieves the associated comment's ID upon click.
     * - Fetches the content of the corresponding comment.
     * - Populates the `commentText` input/textarea with the comment's content for editing.
     * - Updates the submit button's text to "Update".
     * - Sets the form's action attribute to the `edit_comment/{commentId}` endpoint.
     */
    for (let button of editButtons) {
      button.addEventListener("click", (e) => {
        let commentId = e.target.getAttribute("data-comment_id");
        let commentContent = document.getElementById(`comment${commentId}`).innerText.trim();
        commentText.value = commentContent;
        submitButton.innerText = "Update";
        commentForm.setAttribute("action", `/edit_comment/${commentId}/`); 
        console.log("edit button pressed");
      });
    }
}

if (deleteConfirm === null) {
    console.error("Element with ID 'deleteConfirm' not found");
}