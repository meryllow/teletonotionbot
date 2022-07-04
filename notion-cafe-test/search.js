import { Client } from "@notionhq/client"

    const notion = new Client({ auth: process.env.NOTION_KEY });
    const databaseId = process.env.NOTION_DATABASE_ID;

    (async () => {
        const response = await notion.databases.retrieve({
            database_id: databaseId
        });
        console.log(response);
    })();