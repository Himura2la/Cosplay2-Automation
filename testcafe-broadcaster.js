import { Selector } from 'testcafe';


const event_name = 'tulafest'
const token = '___Bake_a_Cookie___'

const message1 = "Напоминаем, что Ваша заявка на Тульский фест YnO еще не до конца оформлена, а досыл закрывается в это воскресенье. Подробности на к2."
const message2 = "Добрый вечер! Пожалуйста, заполните все необходимые поля заявки на Тульский фест Yuki no Odori до 21.01.18, иначе она будет автоматически отклонена и организаторам будет Очень грустно Т_Т. Со своей стороны, делимся с вами (пока) тайной информацией, что датой фестиваля назначено 17 февраля. Сообщить это публично мы сможем уже очень скоро, но Вы узнаёте дату в числе первых. Очень ждём Вашего досыла ^_^"


var start_i = 11  // If it fails in da middle, you can continue
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
            if (j > 3) break
            console.log(`(${i}, ${j}) `, await nums.nth(j).innerText)
            await t.click(nums.nth(j))
            // In a request
            var status = await Selector('a[editable-select="$ctrl.request.status"]').innerText
            console.log(status)
            if (status.indexOf("НУЖЕН ВАШ ОТКЛИК") > 0 || status.indexOf("НУЖНЫ ДОПОЛНИТЕЛЬНЫЕ МАТЕРИАЛЫ") > 0){
                await t
                    .click(Selector('a[ng-click="$ctrl.newCommentFormVisible = true"]'))
                    .typeText(Selector('textarea[ng-model="$ctrl.newCommentForm.comtext"]'), message1)
                    //.click(Selector('input[ng-model="$ctrl.newCommentForm.email"]'))
                    .click(Selector('input[ng-model="$ctrl.newCommentForm.sms"]'))
                    .click(Selector('button[type=submit]'))  // Жмем кнопку "Отправить"
                
                var last_comment = Selector('tr[ng-repeat="comment in $ctrl.comments track by comment.id"]')
                                    .find('span[ng-bind-html="comment.content | htmltext"]').nth(-1)
                await t.expect(last_comment.innerText).eql(message1)  // Проверяем, что отправилось
            
            await t
                .click(Selector('a[ng-click="$ctrl.newCommentFormVisible = true"]'))
                    .typeText(Selector('textarea[ng-model="$ctrl.newCommentForm.comtext"]'), message2)
                .click(Selector('input[ng-model="$ctrl.newCommentForm.email"]'))
                    .click(Selector('input[ng-model="$ctrl.newCommentForm.sms"]')) // СНИМАЕМ чекбокс
                    .click(Selector('button[type=submit]'))  // Жмем кнопку "Отправить"
                
                last_comment = Selector('tr[ng-repeat="comment in $ctrl.comments track by comment.id"]')
                                .find('span[ng-bind-html="comment.content | htmltext"]').nth(-1)
                await t.expect(last_comment.innerText).eql(message2)  // Проверяем, что отправилось
                
            
                console.log("Sent!")
            //await t.debug()
            }
        }
        start_j = 0
    }
})
