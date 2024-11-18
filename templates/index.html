<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sağlık AI Asistanı</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold text-center mb-8">Sağlık AI Asistanı</h1>
        
        <div class="max-w-2xl mx-auto">
            <div class="mb-6">
                <label for="serviceType" class="block text-sm font-medium text-gray-700 mb-2">Hizmet Seçin</label>
                <select id="serviceType" class="w-full p-3 border border-gray-300 rounded-md shadow-sm">
                    <option value="diagnosis">Hastalık Teşhis & Hastane Yönlendirme</option>
                    <option value="psychologist">AI Psikolog Asistanı</option>
                    <option value="aesthetic">Estetik İşlem Planlayıcı</option>
                    <option value="vacation">Tatil Fırsat Avcısı</option>
                    <option value="opportunity">Fırsat Analiz Motoru</option>
                </select>
            </div>
            
            <div class="mb-6">
                <label for="userInput" class="block text-sm font-medium text-gray-700 mb-2">Durumunuzu Anlatın</label>
                <textarea 
                    id="userInput" 
                    rows="5" 
                    class="w-full p-3 border border-gray-300 rounded-md shadow-sm"
                    placeholder="Lütfen detaylı bilgi girin..."></textarea>
            </div>
            
            <button 
                onclick="generateResponse()" 
                class="w-full bg-blue-600 text-white p-3 rounded-md hover:bg-blue-700 transition-colors">
                Analiz Et
            </button>
            
            <div id="loading" class="hidden mt-8 text-center">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                <p class="mt-2 text-gray-600">Analiz yapılıyor...</p>
            </div>
            
            <div id="response" class="hidden mt-8">
                <div class="bg-white p-6 rounded-lg shadow-md">
                    <h2 class="text-xl font-bold mb-4">Sonuç</h2>
                    <div id="responseContent" class="prose prose-blue max-w-none"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
    async function generateResponse() {
        const loading = document.getElementById('loading');
        const responseDiv = document.getElementById('response');
        const responseContent = document.getElementById('responseContent');
        const serviceType = document.getElementById('serviceType').value;
        const userInput = document.getElementById('userInput').value;

        if (!userInput.trim()) {
            alert('Lütfen durumunuzu anlatın');
            return;
        }

        // UI'ı hazırla
        loading.classList.remove('hidden');
        responseDiv.classList.add('hidden');
        responseContent.textContent = '';

        try {
            const response = await fetch('/api/service', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    service_type: serviceType,
                    input: userInput
                })
            });

            const data = await response.json();

            if (data.success) {
                responseContent.textContent = data.response;
                responseDiv.classList.remove('hidden');
            } else {
                alert('Üzgünüm, bir hata oluştu: ' + (data.error || 'Bilinmeyen hata'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Bir bağlantı hatası oluştu. Lütfen tekrar deneyin.');
        } finally {
            loading.classList.add('hidden');
        }
    }
    </script>
</body>
</html>
