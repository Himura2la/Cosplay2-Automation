import { Selector } from 'testcafe';


const event_name = 'tulafest'
const token = '___Bake_a_Cookie___'

const message = 'Новый TestCafe -- Aгонь!!'

const start_i = 0  // If it fails in da middle, you can continue
const start_j = 0

fixture `Broadcaster`.page `http://${event_name}.cosplay2.ru/orgs`;

test('Write to All', async t => {
    await t.eval(() => document.cookie = `auth_ssid=${token}; path=/; domain=${event_name}.cosplay2.ru`, 
                 {dependencies: { event_name, token }})
    await t.navigateTo(`http://${event_name}.cosplay2.ru/orgs/requests/stats`)

    const root_noms = Selector('table.req_stat').find('a')
    const noms_count = await root_noms.count
    await t.click(root_noms.nth(start_i)) // Open the first nom

    for (var i = start_i; i < noms_count; i++){
        var side_topics = Selector('div[ng-controller="fest.orgs.requests.side_topics.Ctrl"')
        var noms = side_topics.find('a[ng-bind="topic.title"]')

        console.log(`(i->${i}) `, await noms.nth(i).innerText)
        if (i != start_i)
            await t.click(await noms.nth(i))  // Open the next nom
        
        var nums = side_topics.find('a').withText('№')
        var nums_count = await nums.count
        for (var j = start_j; j < nums_count; j++){
            console.log(`(${i}, ${j}) `, await nums.nth(j).innerText)
            await t.click(nums.nth(j))
            
            // In the request
            await t
                .click(Selector('a[ng-click="$ctrl.newCommentFormVisible = true"]'))
                .typeText(Selector('textarea[ng-model="$ctrl.newCommentForm.comtext"]'), message)
                .click(Selector('input[ng-model="$ctrl.newCommentForm.email"]'))
            //   .click(Selector('button[type=submit]'))
            //const last_comment = Selector('span[ng-bind-html="comment.content | htmltext"]').nth(-1)
            //await t.expect(last_comment.innerText).eql(message)
            
            //await t.debug()
            
        }
    }
})
