
 <?php if ($page == 0) { ?>
	 <div class="nodePreview<?php print ($sticky) ? " sticky" : ""; ?>">
	  <?php if ($title != ""): ?>
	  
	  <h2><div class="cornerR_yellow"></div>
	  
	  <a href="<?php print $node_url ?>" title="<?php print $title ?>">
	  <?php print $title ?></a>
	  </h2>
	  
	
	  <?php endif; ?>

	
	  <div class="content">
	  <div style="float:left"><?php print $taxonomy_images[0]; ?></div>
	  <?php print $content ?>
	  </div>
	  <?php if ($links): ?>

	  <div class="links"><?php print $links ?></div>
	  <?php endif; ?>
	</div>


  <?php } else { ?>
  
  
  <?php if ($title != ""): ?>
  <div id="title"><div class="cornerR_yellow"></div>
  <h1>
  <?php print $title ?>
  </h1>

  </div>

  <?php endif; ?>



  <div class="content"><div id="article_sidebar"></div>
  <p><strong>Classified Type:</strong> <?php print $taxonomy['taxonomy_term_85']['title']; ?></p>
  <p><strong>Region:</strong> <?php print $taxonomy['taxonomy_term_12']['title']; ?></p>
  
  <?php print $content ?>
  <br />
    <p><em><?php print $submitted; ?> </em></p>
  </div>
  <?php global $user;
  $nodedata=unserialize($node->data); 
	$node_privatemsg_allow = $nodedata['privatemsg_allow'];
  if ($node_privatemsg_allow) 
		print '<br />' . l('contact by private message','privatemsg/msgto/'.$node->uid,array('title'=>'Send a private message.'));
  
  ?>
  <?php if ($links): ?>
  <div class="links"><?php print $links ?></div>
  <?php endif; ?>
  <?php } ?>

  
