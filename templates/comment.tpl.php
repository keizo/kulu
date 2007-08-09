<?php
 $name = $comment->name;
 //print var_dump($comment);
?>




<div class="forum-side"><strong><?php print l($name,'user/'.$comment->uid) ?></strong>
	 <div class="picture"><?php print $picture ?></div>
	 <?php global $user;
	 if ($comment->privatemsg_allow  && $user->uid) 
		print '<br />' . l('contact','privatemsg/msgto/'.$comment->uid,array('title'=>'Send a private message.')); 
	  ?>
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
      <br class="clear" />

      <p><em>
	  <?php print  format_date($comment->timestamp); ?></em> 
	  <?php global $user; 
	  
	  if (($comment->cid && $comment->uid == $user->uid) || ($comment->cid && in_array('super user',$user->roles))) 
	  print '<br />' . l('edit','comment/edit/'.$comment->cid); ?>
	  </p>
    </div>
</div>

<br class="clear" />
