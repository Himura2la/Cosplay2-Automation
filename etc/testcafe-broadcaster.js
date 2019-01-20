import { Selector } from 'testcafe';


const event_name = 'tulafest'
const token = '__BAKE_A_COOKIE___'

const message1 = `Репетиции:
- Пятница, 16 февраля — с 16:00 до 19:30
- Суббота, 17 февраля — с 9:00 до 11:30

Если у Вас есть хоть малейшая возможность придти в пятницу, вы скорее всего порепетируете. В день феста такая возможность совершенно не гарантирована, ибо желающих будет очень много, а времени очень мало.`


var start_i = 0  // If it fails in da middle, you can continue
var start_j = 0

fixture `Broadcaster`.page `http://${event_name}.cosplay2.ru/orgs`;

test('Write to All', async t => {
    await t.eval(() => document.cookie = `auth_ssid=${token}; path=/; domain=${event_name}.cosplay2.ru`, 
                 {dependencies: { event_name, token }})
    await t.navigateTo(`http://${event_name}.cosplay2.ru/orgs/requests/stats`)

    const root_noms = Selector('table.req_stat').find('a')
    const noms_count = await root_noms.count
    await t.click(root_noms.nth(start_i)) // Open the first nom

    for (var i = start_i; i < noms_count; i++){
        var side_topics = Selector('div[ng-controller="fest.orgs.requests.side_topics.Ctrl"]')
        var noms = side_topics.find('a[ng-bind="topic.title"]')
        var nom = await noms.nth(i).innerText
        console.log(`(i->${i}) `, nom)
        if (nom == "ART") // nom protection
            break
        if (i != start_i)
            await t.click(await noms.nth(i))  // Open the next nom
        
        var nums = side_topics.find('div.request')
        var nums_count = await nums.count
        for (var j = start_j; j < nums_count; j++){
            var req_item = nums.nth(j)
            var voting_number = await req_item.find('span[ng-show="request.voting_number"]').find('b').innerText
            var num = await req_item.find('a').innerText
            var status = await req_item.find('img').getAttribute('status')
            console.log(`(${i}, ${j}) `, num)

            if (status != 'approved'){
                console.log('Status:', status + '. Skipping.')
                continue
            }

            await t.click(req_item.find('a'))
            // In a request

            voting_number = (await Selector('span[ng-show="$ctrl.request.voting_number"]').innerText).replace(", ", "")
            const message = message1.replace('{num}', voting_number)

            //await t.debug()
            // await t
            //     .click(Selector('button[ng-click="confirmDelete=true"]').nth(-1))
            //     .click(Selector('button[ng-click="$ctrl.commentDelete(comment.id)"]').nth(-1))


            await t
                .click(Selector('a[ng-click="$ctrl.newCommentFormVisible = true"]'))
                .typeText(Selector('textarea[ng-model="$ctrl.newCommentForm.comtext"]'), message.trim(), {'paste': true})
                //.click(Selector('input[ng-model="$ctrl.newCommentForm.email"]'))
                .click(Selector('button[type=submit]'))  // Жмем кнопку "Отправить"

            console.log("Sent!")

        }
        start_j = 0
    }
})
