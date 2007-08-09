<?php  $nodedata=unserialize($node->data); 
	$node_privatemsg_allow = $nodedata['privatemsg_allow'];
	global $user; 
?>
<?php
  if (!_is_forum()) {
    include('node.tpl.php');
    return;
  }
  $curr_user = user_load(array('uid' => $userid));
  $sig = $curr_user->signature;

  if ($node->title) print '<h1>' . $title . '</h1>';
  if (!$user->uid && !$comment->cid) print '<div class="links">' . $links . '</div>';
?>
<div class="forum-side"><strong><?php print $name ?></strong>
	 <div class="picture"><?php print $picture ?></div>
	    <?php if (module_exists('flatforum')): ?>
        <?php print t('Joined ') . ' ' . $joined; ?><br />
        <?php print $posts . t(' Posts'); ?>
    	<?php endif ?>
		<?php if ($node_privatemsg_allow  && $user->uid) 
				print '<br />' . l('contact','privatemsg/msgto/'.$node->uid,array('title'=>'Send a private message.'));
			if ($comment->privatemsg_allow  && $user->uid) 
				print '<br />' . l('contact','privatemsg/msgto/'.$comment->uid,array('title'=>'Send a private message.')); ?>
</div>
<div class="comment forum-comment comment-<?php print $row_class; print $comment->new ? ' comment-new forum-comment-new' : ''; ?>">

    
    <?php if ($comment->new) : ?>
      <a id="new"></a>
      <span class="new"><?php print $new ?></span>
    <?php endif ?>
    <div class="content">
      <?php print $content ?>
      <?php if ($sig): ?>
        <div class="author-signature">--<br /><?php print check_markup($sig); ?></div>
      <?php endif ?>

      <p><em>
	  <?php print $submitted ?></em> 
	  <?php 
	  if (($comment->cid && $comment->uid == $user->uid) || ($comment->cid && in_array('super user',$user->roles))) 
	  print '<br />' . l('edit','comment/edit/'.$comment->cid); ?>
	  </p>
    </div>

</div>

<br class="clear" />
