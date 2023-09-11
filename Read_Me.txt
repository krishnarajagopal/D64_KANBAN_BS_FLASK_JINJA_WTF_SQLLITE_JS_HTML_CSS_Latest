create DB with the following Fields - DONE
  ID, Title, Description, Assignee, Status, Percent_complete

Create cards in the canvas based on the status. - DONE

Cards to be rendered as per the Due date  sorted ascending (closest data is first) -DONE

Render the title,Assignee Initials, Percent_complete in the Card Front and description, Edit and delete options in the back of card - DONE

Flip the card horizontally to show the description in the Card Back  with auto scroll  when the mouse hovers over the card - DONE

Edit form to be rendered  in a Modal with all the DB details for the specific card- DONE

Ability to Validate all the DB details for the specific card - DONE
 - I tried to get the Server side validation using the flask-bootstrap validations  to work in the update Modal without any Luck.
 - Hence reverted to the client side bootstrap validation to work in the update Modal.
 - It turned out amazing.
 - Also, I ended up with listing out the elements instead of using the render_field method as it proved to be cumbersome

Changing edit form and submitting the Modal should update the DB and the all cards details and status refreshed as per the latest update -  DONE

Drag and drop of the card should update the DB with the latest status of the card and refresh the page- DONE
  -This needs Jquery  AJAX. Hence moved the slim version of the Jquery to Min version
  -Encountered CSRF issues while posting (ID and New Status) data. So had to include the Meta tag of the CSRF token to the Base.html and  include the AJAX setup and AJAX xhr request  code in the script.js file 
  -Found out that the Fetch API is more more mordern and efficient. However, reserved it for later enhancement.

Alert After successful DB update should  be updated and disappear automatically after few seconds -DONE
  - Alert had to have flash messages routed.
  -Implemented Automatic alert closure using Jquery

Ability to delete the card in the back of the card with a confirmation message.-DONE
  - Implemented Delete modal for each card in the card using the delete_modal macro
  -Created a new /Delete POST route to the back end with the ID of the task from the Delete modal submit button.
  -Deleted the record in the and published the confirmation as a flash message using the earler flash message route.

Ability to Add new cards under each of the Status Swim Lanes- DONE
  -Added common Add Buttons to all the swimlane containers
  -Added new create modal by leveraging the existing update modal
  - Changed the Jquery to locate the Container element for updating staus based on drag and drop

Refactor the code as per the flask best practices -LATER ENHANCEMENT

