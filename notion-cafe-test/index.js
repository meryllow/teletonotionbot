import { Client } from "@notionhq/client"
import * as dotenv from 'dotenv'

dotenv.config()

const notion = new Client({ auth: process.env.NOTION_KEY })

const databaseId = process.env.NOTION_DATABASE_ID

async function addItem(text, location) {
    try {
        const response = await notion.pages.create({
            parent: { database_id: databaseId },
            properties: {
                'title': {
                    // id: 'title',
                    // type: "title",
                    title:[
                    {
                        type: "text",
                        text: {
                            "content": text
                        }
                    }
                    ]
                },
                "pyuU": {
                    rich_text: [
                        {
                            text: {
                                "content": location
                            }
                        }
                    ]
                }
                // 'conquered?': {
                //     id: 'G%3ApN',
                //     type: 'checkbox',
                //     checkbox: false 
                // },
                // rating: {
                //     id: '%60W%3FY',
                //     type: 'select',
                //     select: null
                // },
                // remarks: {
                //     id: '%5EA%7DO',
                //     type: 'rich_text',
                //     rich_text: []
                // }
                // link: {
                    //     id: 'lKzO',
                    //     name: 'link',
                    //     type: 'url',
                    //     url: {} 
                    // }
            },
        })
    console.log(response)
    console.log("Success! Entry added.")
    } catch (error) {
    console.error(error.body)
    }
}

addItem("penny university", "east coast")