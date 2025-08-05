<!-- src/lib/components/BookingWidget.svelte -->
<script>
  import { onMount } from 'svelte';
  export let intake; // { id, first_name, last_name, email, ... }

  onMount(() => {
    // Create cal.com booking URL with prefilled data (using local cal.com)
    const calUrl = new URL('http://localhost:3000/nexirahealth/introductory-consultation');
    
    // Add user data as URL parameters (cal.com will prefill the form)
    calUrl.searchParams.set('name', `${intake.first_name} ${intake.last_name}`);
    calUrl.searchParams.set('email', intake.email);
    
    // Add intake ID to metadata so webhook can link booking back to this record
    calUrl.searchParams.set('metadata', JSON.stringify({ intakeId: intake.id }));
    
    // Redirect user to cal.com booking page
    window.location.href = calUrl.toString();
  });
</script>

<div class="booking-card">
  <div class="booking-header">
    <h2>Redirecting to Booking...</h2>
    <p>Hi {intake.first_name}! Taking you to the booking page now.</p>
  </div>
  
  <div style="padding: 2rem; text-align: center;">
    <p>If you're not automatically redirected, <a href="http://localhost:3000/nexirahealth/introductory-consultation">click here</a>.</p>
  </div>
</div>
