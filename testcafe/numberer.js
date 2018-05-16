import { Selector } from 'testcafe';

var nums_converter = require("C:\\Users\\glago\\Desktop\\nums_converter.json")

const event_name = 'tulafest'
const token = '__BAKE_A_COOKIE___'

var start_i = 11  // If it fails in da middle, you can continue
var start_j = 0

fixture `Numberer`.page `http://${event_name}.cosplay2.ru/orgs`;

test('Give everyone a number', async t => {
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
        if (nom == "Фотокосплей") // nom protection
            break
        if (i != start_i)
            await t.click(await noms.nth(i))  // Open the next nom
        
        var nums = side_topics.find('div.request')
        var nums_count = await nums.count
        for (var j = start_j; j < nums_count;){
            // Staying on the first item
            var req_item = nums.nth(j)
            var existing_voting_number = await req_item.find('span[ng-show="request.voting_number"]').find('b').innerText
            var num = await req_item.find('a').innerText
            var voting_number = num.match(/\d+/)[0]
            console.log(`(${i}, ${j}) `, num)

            if (existing_voting_number != voting_number){
                console.log("Skip")
                j++  // Until we get here
                continue
            }

            const target_data = nums_converter.find((e) => e['s_num'] == existing_voting_number)
            if (target_data == undefined){
                console.log("Not found № " + existing_voting_number + " in converter")
                j++
                continue
            }
            voting_number = target_data['t_num']

            await t.click(req_item.find('a'))

            // --- In a request ---
            
            await t
                    .click(Selector('a[editable-number="$ctrl.request.voting_number"]'))
                    .pressKey('ctrl+a')
                    .typeText(Selector('form.form-inline.editable-number').find('input'), voting_number)
                    .click(Selector('form.form-inline.editable-number').find('button[type="submit"]'))

            console.log(`->`, await Selector('a[editable-number="$ctrl.request.voting_number"]').innerText)
            //await t.debug()
        }
        start_j = 0
    }
})
