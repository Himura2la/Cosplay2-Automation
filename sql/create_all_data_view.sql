drop view if exists ALL_DATA;
create view ALL_DATA as
select
	requests.number,
	list.title as type,
	voting_title as title,
	section_title as section,
	[values].title as key, value
from list, requests, [values]
where list.id = topic_id and requests.id = request_id