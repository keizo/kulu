<?php //if(($user->profile_name) != ''): /* check to see if name is set */?>
<div class="box">
<?php if(!empty($user->picture)): ?>
<div class="picture">
<?php print l("<img src=\"http://www.ocpaddler.com/system/files?file=$user->picture\">", 'user/' . $user->uid, array(),NULL,NULL, FALSE, TRUE); ?>

</a>
</div>
<?php endif; ?>
<h3><?php print l($user->name, 'user/' . $user->uid); ?></a><?php 
$time_period = variable_get('user_block_seconds_online', 2700);
if ((time() - $user->access) <= $time_period) print ' (online)'; 
?></h3>
<div class="custom_profiles">
	<?php if (!empty($user->profile_name)): ?>
        <div class="fields">Name: <?php print $user->profile_name; ?></div>
    <?php endif; ?>
    <?php if (!empty($user->profile_location)): ?>
        <div class="fields">Location: <?php print $user->profile_location; ?></div>
    <?php endif; ?>
    <?php if (!empty($user->profile_clubs)): ?>
    <div class="fields">Club(s): <?php print $user->profile_clubs; ?></div>
    <?php endif; ?>
    <?php if (!empty($user->profile_age)): ?>
        <div class="fields">Age: <?php print $user->profile_age; ?></div>
    <?php endif; ?>
</div>
</div>
<?php //endif; ?>
