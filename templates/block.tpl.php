<div class="block block-<? print $block->module?>" id="block-<?php print $block->module . "-" . $block->delta ?>">
<?php if ($block->subject): ?><h2 class="small title"><?php print $block->subject ?></h2><?php endif;?>
<div class="content"><?  print $block->content ?></div>
</div>

