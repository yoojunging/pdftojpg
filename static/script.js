// 파일 위치: static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const resultSection = document.getElementById('result-section');
    const imagePreview = document.getElementById('image-preview');
    const downloadLink = document.getElementById('download-link');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const fileInput = document.getElementById('pdf-file');
        const file = fileInput.files[0];

        if (!file) {
            alert("PDF 파일을 선택해주세요!");
            return;
        }

        const formData = new FormData();
        formData.append('pdf_file', file);

        try {
            const response = await fetch('/convert', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('서버 오류 또는 변환 실패');
            }

            const data = await response.json();

            // 변환된 이미지들을 화면에 표시
            imagePreview.innerHTML = '';
            data.image_urls.forEach(url => {
                const img = document.createElement('img');
                img.src = url;
                imagePreview.appendChild(img);
            });

            // 다운로드 링크 설정
            downloadLink.href = data.zip_url;

            // 결과 섹션 보여주기
            resultSection.style.display = 'block';
        } catch (error) {
            alert('에러 발생: ' + error.message);
        }
    });
});
