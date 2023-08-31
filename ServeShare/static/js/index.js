document.addEventListener("DOMContentLoaded", function () {
    // Toggle comment section visibility
    const toggleCommentButtons = document.querySelectorAll(".toggle-comment");
    toggleCommentButtons.forEach(button => {
        button.addEventListener("click", function () {
            const commentSection = this.closest(".box").querySelector(".comment-section");
            commentSection.style.display = commentSection.style.display === "none" ? "block" : "none";

            if(this.classList.contains("fa-comment"))
            {
                this.classList.remove("fa-comment");
                this.classList.add("fa-comment-dots");
            }
            else{
                this.classList.add("fa-comment");
                this.classList.remove("fa-comment-dots");
            }

        });
    });

    // Toggle heart icon color and count likes
   // Toggle heart icon color and add heartbeat animation
   const heartIcons = document.querySelectorAll(".heart-icon");
   heartIcons.forEach(icon => {
       icon.addEventListener("click", function () {
           const isLiked = this.classList.contains("liked");
           if (isLiked) {
               this.classList.remove("liked");
               this.style.color = "#d5d0d0";
           } else {
               this.classList.add("liked");
               this.style.color = "#00BBFF";
               this.style.animation = "heartbeat 0.3s ease-in-out"; // Add heartbeat animation
           }
           // You can add logic here to update the like count in the backend
       });
   });
});