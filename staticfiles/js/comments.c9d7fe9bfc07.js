document.addEventListener('DOMContentLoaded', function () {
  console.log("DOM fully loaded and parsed.");

  // Assign background colors to comment entries based on their index.
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

  const reviewMessage = document.getElementById("reviewMessage");

  /*
  When a user clicks the submit button, show a message at the top of the page
  indicating that the comment is under review.
  */
  if (submitButton) {
      submitButton.addEventListener("click", function (e) {
          e.preventDefault(); // Prevent the default form submission
          console.log("Submit button clicked");
          
          // Show the review message
          reviewMessage.style.display = "block";

          // Optionally, you can submit the form after showing the message
          setTimeout(function () {
              commentForm.submit();
          }, 2000); // Delay to allow the user to see the message
      });
  }

  /*
  Handle edit button click - similar to previous implementation
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
  Handle delete button click - similar to previous implementation
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
});
