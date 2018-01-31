import { Selector } from 'testcafe';


const event_name = 'tulafest'
const token = ''

const message1 = "Приглашаем Вас проверить расположение своего номера в черновом вариане программы фестиваля: https://docs.google.com/spreadsheets/d/1HkcKL72kTZPipqMU9M-CbKMP2b8p7uH46rtIRIhh42w/edit?usp=sharing Разумеется, время указано приблизительное и на него ни в коем случае на стоит ориентироваться. Номера также будут меняться, чтобы соответствовать порядку выступлений. Если Вас что-то не устраивает в программе, напишите пожалуйста комментарий к Вашей ячейке в таблице. Также, для надёжности, можно написать сюда, Дере VK или мне VK."


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

        console.log(`(i->${i}) `, await noms.nth(i).innerText)
        if (i != start_i)
            await t.click(await noms.nth(i))  // Open the next nom
        
        var nums = side_topics.find('a').withText('№')
        var nums_count = await nums.count
        for (var j = start_j; j < nums_count; j++){
            console.log(`(${i}, ${j}) `, await nums.nth(j).innerText)
            await t.click(nums.nth(j))
            // In a request
            var status = await Selector('a[editable-select="$ctrl.request.status"]').innerText
            console.log(status)
            if (status.indexOf("ЗАЯВКА ПРИНЯТА") > 0){
                await t
                    .click(Selector('a[ng-click="$ctrl.newCommentFormVisible = true"]'))
                    .typeText(Selector('textarea[ng-model="$ctrl.newCommentForm.comtext"]'), message1)
                    .click(Selector('input[ng-model="$ctrl.newCommentForm.email"]'))
                    //.click(Selector('input[ng-model="$ctrl.newCommentForm.sms"]'))
                    .click(Selector('button[type=submit]'))  // Жмем кнопку "Отправить"
                
                var last_comment = Selector('tr[ng-repeat="comment in $ctrl.comments track by comment.id"]')
                                    .find('span[ng-bind-html="comment.content | htmltext"]').nth(-1)
                await t.expect(last_comment.innerText).eql(message1)  // Проверяем, что отправилось
            
          //  await t
          //      .click(Selector('a[ng-click="$ctrl.newCommentFormVisible = true"]'))
          //          .typeText(Selector('textarea[ng-model="$ctrl.newCommentForm.comtext"]'), message2)
          //      .click(Selector('input[ng-model="$ctrl.newCommentForm.email"]'))
          //          .click(Selector('input[ng-model="$ctrl.newCommentForm.sms"]')) // СНИМАЕМ чекбокс
          //          .click(Selector('button[type=submit]'))  // Жмем кнопку "Отправить"
          //      
          //      last_comment = Selector('tr[ng-repeat="comment in $ctrl.comments track by comment.id"]')
          //                      .find('span[ng-bind-html="comment.content | htmltext"]').nth(-1)
          //      await t.expect(last_comment.innerText).eql(message2)  // Проверяем, что отправилось
                
            
                console.log("Sent!")
            await t.debug()
            }
        }
        start_j = 0
    }
})
