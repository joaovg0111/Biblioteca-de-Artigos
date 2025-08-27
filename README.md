Claro! Aqui está a versão modificada do projeto, atualizada com as informações do novo grupo e os requisitos da biblioteca digital de artigos.

# 📚 Biblioteca Digital de Artigos

Este projeto tem como objetivo desenvolver uma **biblioteca digital** para disponibilizar **acesso fácil e centralizado aos artigos publicados** em determinados eventos científicos. A plataforma será um repositório organizado, permitindo que usuários encontrem e acessem produções acadêmicas de forma eficiente.

As principais inspirações para o desenvolvimento são plataformas consagradas como:
- **ACM Digital Library**
- **SBC Open-Lib**
- **arXiv.org**
- **dblp.org**

Nosso objetivo é criar uma ferramenta robusta para a comunidade acadêmica, facilitando a disseminação do conhecimento científico.

---

## 👥 Membros da Equipe e Papéis

| Nome | Matrícula | Papel |
|--------------|------------|-----------|
| João | 2019027695 | Fullstack |
| Luis | - | Fullstack |
| Seungbin Han | - | Fullstack |

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python
- **Backend**: Django
- **Frontend**: HTML + CSS
- **Banco de Dados**: SQLite

---

## 📌 Backlog do Produto

- Como administrador, eu quero cadastrar, editar e deletar um evento.
- Como administrador, eu quero cadastrar, editar e deletar uma nova edição de um evento.
- Como administrador, eu quero cadastrar, editar e deletar um artigo manualmente, incluindo seu PDF.
- Como administrador, eu quero cadastrar artigos em massa a partir de um arquivo BibTeX.
- Como usuário, eu quero pesquisar artigos por título, autor e nome do evento.
- Como administrador, eu quero que todo evento tenha uma home page com suas edições, e que cada edição tenha uma home page com seus artigos.
- Como usuário, eu quero ter uma home page com os meus artigos, organizados por ano.
- Como usuário, eu quero me cadastrar para receber um e-mail sempre que um novo artigo de meu interesse for disponibilizado.

---

## 📆 Backlog da Sprint

### Fundações do Projeto
- Instalar frameworks e criar a estrutura inicial da aplicação.
- Instalar e configurar o banco de dados.
- Definir o Modelo Entidade-Relacionamento (MER) para eventos, edições e artigos.
- Criar os modelos (models) no Django e aplicar as migrações no banco de dados.

### História 1: Como administrador, eu quero cadastrar (editar, deletar) um evento e suas edições.
- Implementar as funcionalidades de CRUD (Create, Read, Update, Delete) para eventos.
- Implementar as funcionalidades de CRUD para as edições de um evento.
- Criar a interface no painel de administração do Django para gerenciar eventos e edições.

### História 2: Como administrador, eu quero cadastrar um artigo manualmente, incluindo seu pdf.
- Implementar a funcionalidade de CRUD para artigos.
- Criar um formulário para upload de artigos e seus respectivos arquivos PDF.
- Implementar a lógica no backend para salvar o artigo e o arquivo associado.

### História 3: Como usuário, eu quero pesquisar por artigos: por título, por autor e por nome de evento.
- Criar a interface de busca principal na página inicial.
- Implementar a lógica de busca no backend para filtrar artigos pelos critérios especificados (título, autor, evento).
- Desenvolver a página de resultados para exibir os artigos encontrados.
