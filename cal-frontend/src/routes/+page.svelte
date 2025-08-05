<script>
  import IntakeForm from '$lib/components/IntakeForm.svelte';
  import BookingWidget from '$lib/components/BookingWidget.svelte';

  // Holds the saved Intake record
  let intake = null;

  // Called when IntakeForm dispatches the created object
  function handleSuccess(event) {
    intake = event.detail;
  }
</script>

{#if !intake}
  <!-- Show the form until we've created an intake -->
  <IntakeForm on:success={handleSuccess} />
{:else}
  <!-- Once intake exists, render the booking widget -->
  <BookingWidget {intake} />
{/if}
