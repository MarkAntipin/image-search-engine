CREATE or REPLACE FUNCTION vector_norm(IN vector double precision[])
    RETURNS double precision AS
$BODY$
BEGIN
    RETURN(SELECT SQRT(SUM(pow)) FROM (SELECT POWER(e, 2) as pow from unnest(vector) as e) as norm);
END;
$BODY$ LANGUAGE 'plpgsql';



CREATE OR REPLACE FUNCTION dot_product(IN vector1 double precision[], IN vector2 double precision[])
    RETURNS double precision
AS $BODY$
BEGIN
    RETURN(SELECT sum(mul) FROM (SELECT v1 * v2 as mul FROM unnest(vector1, vector2) AS t(v1, v2)) AS denominator);
END;
$BODY$ LANGUAGE 'plpgsql';



CREATE OR REPLACE FUNCTION cosine_similarity(IN vector1 double precision[], IN vector2 double precision[])
    RETURNS double precision
AS $BODY$
BEGIN
    RETURN(select ((select dot_product(vector1, vector2) as dot_pod) /
                   ((select vector_norm(vector1) as norm1) *
                    (select vector_norm(vector2) as norm2))) AS similarity_value);
END;
$BODY$ LANGUAGE 'plpgsql';
