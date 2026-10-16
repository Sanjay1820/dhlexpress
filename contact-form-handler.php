<?php 
$errors = '';
$myemail = 'info@dhlrexpress.com';//<-----Put Your email address here.
if(empty($_POST['name'])  || 
   empty($_POST['mobile']) || 
   empty($_POST['email']) || 
      empty($_POST['message']))
{
    $errors .= "\n Error: all fields are required";
}

$name = $_POST['name']; 
$mobile = $_POST['mobile']; 
$email_address = $_POST['email']; 
$message = $_POST['message']; 

if (!filter_var($email_address, FILTER_VALIDATE_EMAIL))
{
    $errors .= "\n Error: Invalid email address";
}

if( empty($errors))
{
	$to = $myemail; 
	$email_subject = "Contact form submission: $name";
	$email_body = "You have received a new message From www.dhlrexpress.com".
	" Here are the details:\n Name: $name \n Mobile: $mobile \n Email: $email_address \n Message \n $message"; 
	
	$headers = "From: $myemail\n"; 
	$headers .= "Reply-To: $email_address";
	
	mail($to,$email_subject,$email_body,$headers);
	//redirect to the 'thank you' page
	header('Location: thanks.html');
} 
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"> 
<html>
<head>
	<title>Contact form handler</title>
    

</head>

<body>
<!-- This page is displayed only if there is some error -->
<?php
echo nl2br($errors);
?>


</body>
</html>