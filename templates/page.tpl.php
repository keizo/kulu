<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html lang="<?php print $language ?>" xml:lang="<?php print $language ?>" xmlns="http://www.w3.org/1999/xhtml">
<head>
 <title><?php print $head_title ?></title>
 <?php print $head ?>
 <style type="text/css" media="screen">
  
	@import url(/<?php print path_to_theme()."/layout.css"; ?>);
	@import url(/<?php print path_to_theme()."/style.css"; ?>);
  
 </style>
 <?php print $styles ?>
<script type="text/javascript"><!--//--><![CDATA[//><!--

sfHover = function() {
	var sfEls = document.getElementById("nav").getElementsByTagName("LI");
	for (var i=0; i<sfEls.length; i++) {
		sfEls[i].onmouseover=function() {
			this.className+=" sfhover";
		}
		sfEls[i].onmouseout=function() {
			this.className=this.className.replace(new RegExp(" sfhover\\b"), "");
		}
	}
}
if (window.attachEvent) window.attachEvent("onload", sfHover);

//--><!]]></script>
</head>
<body>

<?php print theme("onload_attribute"); ?>

<div id="header">
	<div id="logo"><a href="/"><img src="/themes/ocp10/images/logo.png" alt="OCPaddler.com" width="230" height="50" /></a></div>
	<div id="nav">
		<ul class="nav">
			<li><a href="/forum">forum</a></li>
			<li><a href="/gallery">photos</a></li>
			<li><a href="/videos">videos</a></li>
			<li><a href="/event">calendar</a></li>
			<li><a href="/resources">more&not;</a>
				<ul>
					<li><a href="/articles">articles</a></li>
					<li><a href="/canoeclubs">canoe club list</a></li>
					<li><a href="/classifieds">classifieds</a></li>
					<li><a href="/game">game</a></li>
					<li><a href="/links">links</a></li>
					<li><a href="/popular">popular</a></li>
				</ul> 
			</li>
			<li><a href="/search">search&not;</a>
				<ul class="search-box"><li>
			<form id="search_block_form" method="post" action="/search/node">
<input type="text" class="form-text" title="Enter the terms you wish to search for." value="" size="15" id="edit-search_block_form_keys" name="keys" maxlength="128"/>
<input class="form-submit" type="submit" value="Search" name="op"/>
<input id="edit-search-form" type="hidden" value="search_form" name="form_id"/>
</form>
				</li></ul> 
			</li>
			<!--
			<?php global $user; if ($user->uid) : ?>
			<li><a href="/special">Special</a>
				<ul>
					<li><a href="/paddlers">Paddlers List</a></li>
					<li><a href="/popular">Popular Content</a></li>
					<li><a href="/tracker">Recent Posts</a></li>
					<li><a href="http://www.ocpaddler.com/gallery/?g2_view=comment.ShowAllComments">Photo Comments</a></li>
				</ul>
			</li>
			<?php else: ?>
			<li><a href="/oc1intro">New to oc1?</a></li>
			<?php endif; ?> -->
		</ul>
	</div>
	<div id="user_nav">
		<?php if ($secondary_links || $user->uid) : ?>	
			 <ul>
				<li class="title"><strong> <?php print $user->name; ?> &nbsp;</strong></li>
			  <?php if ($secondary_links): foreach ($secondary_links as $link): ?>
			   <li><?php print theme('links', $secondary_links) ?></li>
			  <?php endforeach; endif; ?>
			  <li><a href="/node/add">Submit</a></li>
			  <li><a href="/user">My Account</a></li>
			  <li<?php if (_privatemsg_get_new_messages()) print ' class="inboxfull"'; ?>><?php print '<a href="/privatemsg"> Inbox (' . _privatemsg_get_new_messages() .')</a>'; ?> </li>

			  <li><a href="/logout">Log Out</a></li>
				   </ul>
				<p>
				<?php
          // Count users with activity in the past defined period.
          $interval = time() - variable_get('user_block_seconds_online', 900);

          // Perform database queries to gather online user lists.  We use s.timestamp
          // rather than u.access because it is much faster is much faster..
          $anonymous_count = sess_count($interval);
          $authenticated_users = db_query('SELECT u.uid, u.name FROM {users} u INNER JOIN {sessions} s ON u.uid = s.uid WHERE s.timestamp >= %d AND s.uid > 0 ORDER BY s.timestamp DESC', $interval);
          $authenticated_count = db_num_rows($authenticated_users);

          // Format the output with proper grammar.
          if ($anonymous_count == 1 && $authenticated_count == 1) {
            $output = t('<a href="/paddlers">%members</a> and %visitors online.', array('%members' => format_plural($authenticated_count, '1 paddler', '@count paddlers'), '%visitors' => format_plural($anonymous_count, '1 guest', '@count guests')));
          }
          else {
            $output = t('<a href="/paddlers">%members</a> and %visitors online.', array('%members' => format_plural($authenticated_count, '1 paddler', '@count paddlers'), '%visitors' => format_plural($anonymous_count, '1 guest', '@count guests')));
          }
	print $output;
				?>
				</p>
		<?php else: ?>
			<form action="<?php print url('user', drupal_get_destination()); ?>" method="post">
			  <div id="login_remember_me">
        <input id="edit-remember-me" class="form-checkbox" type="checkbox" value="1" name="remember_me"/>
			  remember me</div>
			  <div id="login_username">paddler login:
			  <input class="login" type="text" name="name" id="name" size="12" value="username" onFocus="if (this.value == 'username') this.value = '';mypass=document.getElementById('pass');if (mypass.value=='password') {mypass.type='password';mypass.value='';}" />
			
			  <input class="login" name="pass" id="pass" type="text" onFocus="this.type='password';if (this.value == 'password') this.value='';" value="password" size="12" />
			
			  <input id="edit-user-login" type="hidden" value="user_login" name="form_id"/> 
			  <input name="op" type="image" src="/themes/ocp9/images/login_but.gif" value="Log in" />
			  </div>
      </form>
	<?php endif; ?>
	</div>
</div>

<div id="header2">&nbsp;</div>


<div id="frame">
	<div id="main">
				  <?php if ($breadcrumb != '' && $node->type != 'blog') { ?>
				<div id="breadcrumbs">
				  <?php print $breadcrumb;?> <span class="breadcrumb">	&raquo;	 <?php if ($title != ""): print ucwords($title); endif; ?></span>
				</div>
			  <?php } ?>
			 <?php if ($mission != ""): ?>
			  <div id="mission"><span><?php print $mission ?></span></div>
			<?php endif; ?>

			<?php if ($messages != ""): ?>
			  <div id="message"><?php print $messages ?></div>
			<?php endif; ?>
			<?php if ($help != ""): ?>
			  <p id="help"><?php print $help ?></p>
			<?php endif; ?>
		<?php if ($tabs != ""): ?>
		<?php print $tabs ?>
			<?php endif; ?>
		<?php //***********left and right columns for front page
		if (($_GET['q']) == variable_get('site_frontpage','node')){ ?>
			<div id="content">
			<!-- start main content -->
			<?php //outputs block 6 as a header to main content
			$block = module_invoke('block', 'block', 'view', 6);
			print $block['content'];
			?>
			<?php print($content) ?>
			<!-- end main content -->
			
			</div>
			<div id="sidebar">
					<?php print $sidebar_left; ?>
			</div>
		<?php } else { ?>
			<div id="content_span">
			<?php if ($sidebar_left != '') { ?>
			<div id="sidebar_nospan">
					<?php print $sidebar_left; ?>
			</div>
			<?php } ?>
			<!-- start main content -->
			<?php print($content) ?>
			<!-- end main content -->
			</div>
		<?php } ?>
	</div>
	<div id="column3">
		<?php if ($sidebar_right != '') { ?>
			<?php print $sidebar_right; ?>
		<?php } ?>
	</div>
</div>

<div id="footer">
	<ul class="nav">
		<li><a href="/log">WebLog</a></li>
		<li><a href="/about">About</a></li>
		<li><a href="/share">Terms</a></li>
		<li><a href="/rss">RSS</a></li>
		<li><a href="mailto:keizo@ocpaddler.com">email:Keizo</a></li>	  
	</ul>
<div id="footer2">
	<?php if ($footer_message) : ?>
		<p class="small"><?php print $footer_message;?></p>
	<?php endif; ?>
	<?php print $closure;?>




<script src="http://www.google-analytics.com/urchin.js" type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "UA-95250-1";
urchinTracker();
</script>
<p class="small">
<?php 
global $me_starttime;
$me_mtime = explode(' ', microtime());
$me_totaltime = $me_mtime[0] + $me_mtime[1] - $me_starttime;
printf('Page loaded in %.3f seconds.', $me_totaltime);
?>
</p>
</div>
</div>
</body>
</html>

