const updateInfoBtn = document.getElementById('update-info-btn');
        const changePasswordBtn = document.getElementById('change-password-btn');
        const updateInfoForm = document.getElementById('update-info-form');
        const changePasswordForm = document.getElementById('change-password-form');
        const cancelUpdateInfoBtn = document.getElementById('cancel-update-info');
        const cancelChangePasswordBtn = document.getElementById('cancel-change-password');

        updateInfoBtn.addEventListener('click', () => {
            updateInfoForm.style.display = 'block';
            changePasswordForm.style.display = 'none';
        });

        changePasswordBtn.addEventListener('click', () => {
            updateInfoForm.style.display = 'none';
            changePasswordForm.style.display = 'block';
        });

        cancelUpdateInfoBtn.addEventListener('click', () => {
            updateInfoForm.style.display = 'none';
        });

        cancelChangePasswordBtn.addEventListener('click', () => {
            changePasswordForm.style.display = 'none';
        });