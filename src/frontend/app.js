const http = require('http');
const fs = require('fs');
const path = require('path');

// Функция для чтения файла в текущем каталоге
function serveFile(filePath, contentType, response) {
    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                // Если файл не найден, отправляем 404
                response.writeHead(404, { 'Content-Type': 'text/html' });
                response.end('404: File Not Found');
            } else {
                // Внутренняя ошибка сервера
                response.writeHead(500);
                response.end('Sorry, check with the site admin for error: ' + error.code + ' ..\n');
            }
        } else {
            // Если файл найден, отдаем его содержимое
            response.writeHead(200, { 'Content-Type': contentType });
            response.end(content, 'utf-8');
        }
    });
}

// Создаем HTTP сервер
http.createServer((request, response) => {
    let filePath = '.' + request.url;
    if (filePath === './') {
        filePath = './index.html';
    }

    const extname = String(path.extname(filePath)).toLowerCase();
    const mimeTypes = {
        '.html': 'text/html',
        '.js': 'text/javascript',
        '.css': 'text/css',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.wav': 'audio/wav',
        '.mp4': 'video/mp4',
        '.woff': 'application/font-woff',
        '.ttf': 'application/font-ttf',
        '.eot': 'application/vnd.ms-fontobject',
        '.otf': 'application/font-otf',
        '.wasm': 'application/wasm'
    };

    // Определяем Content-Type по расширению файла
    const contentType = mimeTypes[extname] || 'application/octet-stream';

    // Сервируем файл
    serveFile(filePath, contentType, response);

}).listen(8080);

console.log('Server running at http://localhost:8080/');
