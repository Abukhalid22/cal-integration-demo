<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  // Form data matching Django model
  let form = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    date_of_birth: '',
    contact_method: 'email',
    reason_for_visit: '',
    consent: false
  };

  let loading = false;
  let errors = {};

  // Contact method options
  const contactOptions = [
    { value: 'email', label: 'Email' },
    { value: 'phone', label: 'Phone' },
    { value: 'sms', label: 'SMS' }
  ];

  async function handleSubmit(e) {
    e.preventDefault();
    loading = true;
    errors = {};

    try {
      const res = await fetch('/api/intakes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      
      if (res.ok) {
        const data = await res.json();
        dispatch('success', data);
      } else {
        const errorData = await res.json();
        errors = errorData;
      }
    } catch (err) {
      errors = { non_field_errors: ['Network error. Please try again.'] };
    } finally {
      loading = false;
    }
  }

  // Helper function to check if field has error
  function hasError(field) {
    return errors[field] && errors[field].length > 0;
  }

  // Helper function to get error message
  function getError(field) {
    return errors[field] ? errors[field][0] : '';
  }
</script>

<div class="form-card">
  <div class="form-header">
    <h1>New Patient Intake</h1>
    <p>Please fill out this form to get started with your care</p>
  </div>

  <div class="form-content">
    <form class="intake-form" on:submit={handleSubmit}>
      <!-- Personal Information Section -->
      <div class="form-section">
        <div class="form-row">
          <div class="form-group">
            <label class="form-label required" for="first_name">First Name</label>
            <input
              type="text"
              id="first_name"
              class="form-input {hasError('first_name') ? 'error' : ''}"
              bind:value={form.first_name}
              required
              placeholder="Enter your first name"
            />
            {#if hasError('first_name')}
              <div class="form-error">
                <span>⚠</span>
                {getError('first_name')}
              </div>
            {/if}
          </div>

          <div class="form-group">
            <label class="form-label required" for="last_name">Last Name</label>
            <input
              type="text"
              id="last_name"
              class="form-input {hasError('last_name') ? 'error' : ''}"
              bind:value={form.last_name}
              required
              placeholder="Enter your last name"
            />
            {#if hasError('last_name')}
              <div class="form-error">
                <span>⚠</span>
                {getError('last_name')}
              </div>
            {/if}
          </div>
        </div>

        <div class="form-group">
          <label class="form-label required" for="email">Email Address</label>
          <input
            type="email"
            id="email"
            class="form-input {hasError('email') ? 'error' : ''}"
            bind:value={form.email}
            required
            placeholder="Enter your email address"
          />
          {#if hasError('email')}
            <div class="form-error">
              <span>⚠</span>
              {getError('email')}
            </div>
          {/if}
        </div>

        <div class="form-row">
          <div class="form-group">
            <label class="form-label required" for="phone">Phone Number</label>
            <input
              type="tel"
              id="phone"
              class="form-input {hasError('phone') ? 'error' : ''}"
              bind:value={form.phone}
              required
              placeholder="(555) 123-4567"
            />
            {#if hasError('phone')}
              <div class="form-error">
                <span>⚠</span>
                {getError('phone')}
              </div>
            {/if}
          </div>

          <div class="form-group">
            <label class="form-label required" for="date_of_birth">Date of Birth</label>
            <input
              type="date"
              id="date_of_birth"
              class="form-input {hasError('date_of_birth') ? 'error' : ''}"
              bind:value={form.date_of_birth}
              required
            />
            {#if hasError('date_of_birth')}
              <div class="form-error">
                <span>⚠</span>
                {getError('date_of_birth')}
              </div>
            {/if}
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="contact_method">Preferred Contact Method</label>
          <select
            id="contact_method"
            class="form-select {hasError('contact_method') ? 'error' : ''}"
            bind:value={form.contact_method}
          >
            {#each contactOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
          {#if hasError('contact_method')}
            <div class="form-error">
              <span>⚠</span>
              {getError('contact_method')}
            </div>
          {/if}
        </div>

        <div class="form-group">
          <label class="form-label" for="reason_for_visit">Reason for Visit</label>
          <textarea
            id="reason_for_visit"
            class="form-textarea {hasError('reason_for_visit') ? 'error' : ''}"
            bind:value={form.reason_for_visit}
            placeholder="Please describe the reason for your visit or any specific concerns you'd like to discuss..."
            rows="4"
          ></textarea>
          {#if hasError('reason_for_visit')}
            <div class="form-error">
              <span>⚠</span>
              {getError('reason_for_visit')}
            </div>
          {/if}
        </div>

        <!-- Consent Section -->
        <div class="checkbox-group">
          <input
            type="checkbox"
            id="consent"
            class="form-checkbox"
            bind:checked={form.consent}
            required
          />
          <label class="checkbox-label" for="consent">
            I consent to the storage and processing of my personal information for healthcare purposes. 
            I understand that this information will be kept confidential and used only for my medical care.
          </label>
        </div>
        {#if hasError('consent')}
          <div class="form-error">
            <span>⚠</span>
            {getError('consent')}
          </div>
        {/if}

        <!-- General Errors -->
        {#if errors.non_field_errors}
          <div class="form-error">
            <span>⚠</span>
            {errors.non_field_errors[0]}
          </div>
        {/if}

        <!-- Submit Button -->
        <button
          type="submit"
          class="btn btn-primary {loading ? 'btn-loading' : ''}"
          disabled={loading || !form.consent}
        >
          {loading ? '' : 'Continue to Booking'}
        </button>
      </div>
    </form>
  </div>
</div>
