// Importar o módulo mysql
const mysql = require('mysql');

// Configurações da conexão
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'bd_site'
};

// Criar uma conexão com o banco de dados
const connection = mysql.createConnection(dbConfig);

// Conectar ao banco de dados
connection.connect((err) => {
    if (err) {
        console.error('Erro ao conectar ao banco de dados:', err.stack);
        return;
    }
    console.log('Conexão ao banco de dados efetuada com sucesso!');
});

// Fechar a conexão quando não for mais necessária
connection.end();