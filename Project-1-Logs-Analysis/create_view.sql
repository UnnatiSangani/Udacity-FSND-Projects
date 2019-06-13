-- PostgreSQL database View Creation
--

--
-- Name: article_view_summ; Type: view; Schema: public
--

CREATE VIEW article_vw_summ AS
    SELECT substring(path,10) as log_slug, count(*) as view_count 
    FROM log
    WHERE status = '200 OK' and path like '/%/%'
    GROUP BY log_slug
    ORDER BY view_count desc;


--
-- Name: view_log; Type: view; Schema: public
--

CREATE VIEW vw_log AS
    SELECT
        total_req, err_req, log_date
    FROM 
        (select DATE(time) as log_date, count(id) as total_req from log group by log_date) a 
    JOIN
        (select DATE(time) as err_date, count(id) as err_req from log where status = '404 NOT FOUND' group by err_date) b
    on a.log_date = b.err_date;

