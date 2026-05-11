-- Schema base para app_cide
-- Motor objetivo: MySQL 8+

DROP DATABASE IF EXISTS app_cide;
CREATE DATABASE app_cide CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE app_cide;

CREATE TABLE proyecto (
    id_proy INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    cod_proy INT NOT NULL,
    CDF TEXT,
    descrip_proy TEXT,
    fch_registro DATETIME,
    fch_ult_act DATETIME,
    UNIQUE KEY uniq_cod_proy (cod_proy),
    INDEX idx_proyecto_id_proy (id_proy)
) ENGINE=InnoDB;

CREATE TABLE programa (
    cod_prog INT NOT NULL,
    version INT NOT NULL,
    nombre VARCHAR(255),
    nivel VARCHAR(20),
    cant_trim VARCHAR(2),
    fch_sub_prg DATETIME,
    fhc_utl_act_prg DATETIME,
    cod_proy_fk INT NOT NULL,
    PRIMARY KEY (cod_prog, version),
    UNIQUE KEY uniq_prog_cod_prog (cod_prog),
    INDEX idx_programa_cod_proy_fk (cod_proy_fk),
    CONSTRAINT fk_programa_proyecto
        FOREIGN KEY (cod_proy_fk)
        REFERENCES proyecto(id_proy)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE calenda_academico (
    id_cal_acad INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    anio INT NOT NULL,
    actividad VARCHAR(255),
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE
) ENGINE=InnoDB;

CREATE TABLE ficha (
    id_fich INT NOT NULL,
    fecha_inic_lec DATE,
    fecha_fin_lec DATE,
    proy_formativo_enruto TEXT,
    trimestre INT,
    abierta TINYINT NOT NULL DEFAULT 1,
    cerr_convenio VARCHAR(10),
    jornada VARCHAR(255),
    id_cal_acad_fk INT,
    cod_proy_fk INT NOT NULL,
    fch_registro DATETIME,
    fch_ult_act DATETIME,
    PRIMARY KEY (id_fich),
    INDEX idx_ficha_cod_proy_fk (cod_proy_fk),
    INDEX idx_ficha_id_cal_acad_fk (id_cal_acad_fk),
    CONSTRAINT fk_ficha_proyecto
        FOREIGN KEY (cod_proy_fk)
        REFERENCES proyecto(id_proy)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_ficha_calenda_academico
        FOREIGN KEY (id_cal_acad_fk)
        REFERENCES calenda_academico(id_cal_acad)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE ficha_historial (
    id_historial INT NOT NULL AUTO_INCREMENT,
    id_fich_fk INT NOT NULL,
    fecha_inic_lec DATE,
    fecha_fin_lec DATE,
    trimestre INT,
    abierta TINYINT NOT NULL DEFAULT 1,
    CDF TEXT,
    cerr_convenio VARCHAR(255),
    jornada VARCHAR(255),
    tipo_cambio VARCHAR(50) NOT NULL DEFAULT 'CREACION',
    fch_registro DATETIME,
    fch_ult_act DATETIME,
    PRIMARY KEY (id_historial),
    INDEX idx_ficha_historial_id_fich_fk (id_fich_fk),
    CONSTRAINT fk_ficha_historial_ficha
        FOREIGN KEY (id_fich_fk)
        REFERENCES ficha(id_fich)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE horario (
    id_horario INT NOT NULL AUTO_INCREMENT,
    dia VARCHAR(255),
    PRIMARY KEY (id_horario),
    INDEX idx_horario_id_horario (id_horario)
) ENGINE=InnoDB;

CREATE TABLE competencia (
    id_comp INT NOT NULL AUTO_INCREMENT,
    cod_comp INT NOT NULL,
    nombre VARCHAR(255),
    duracion_hora INT,
    id_prog_fk INT NOT NULL,
    PRIMARY KEY (id_comp),
    INDEX idx_competencia_cod_comp (cod_comp),
    INDEX idx_competencia_id_prog_fk (id_prog_fk),
    CONSTRAINT fk_competencia_programa
        FOREIGN KEY (id_prog_fk)
        REFERENCES programa(cod_prog)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE resultado (
    id_resu INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(255),
    duracion_hora_max INT,
    duracion_hora_min INT,
    trim_prog INT,
    hora_sema_programar INT,
    hora_trim_programar INT,
    id_comp_fk INT NOT NULL,
    PRIMARY KEY (id_resu),
    INDEX idx_resultado_id_comp_fk (id_comp_fk),
    CONSTRAINT fk_resultado_competencia
        FOREIGN KEY (id_comp_fk)
        REFERENCES competencia(id_comp)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE vinculacion (
    id_vinculacion INT NOT NULL AUTO_INCREMENT,
    tip_vincul VARCHAR(255),
    nmr_contrato VARCHAR(255),
    nvl_formacion VARCHAR(255),
    pregrado TEXT,
    postgrado TEXT,
    coord_pertenece TEXT,
    modalidad TEXT,
    especialidad TEXT,
    fch_inic_contrato DATE,
    fch_fin_contrato DATE,
    area TEXT,
    estudios TEXT,
    red TEXT,
    fch_registro DATETIME,
    fch_ult_act DATETIME,
    PRIMARY KEY (id_vinculacion),
    INDEX idx_vinculacion_id_vinculacion (id_vinculacion)
) ENGINE=InnoDB;

CREATE TABLE rol (
    id_rol INT NOT NULL AUTO_INCREMENT,
    nombre_rol VARCHAR(255),
    PRIMARY KEY (id_rol),
    INDEX idx_rol_id_rol (id_rol)
) ENGINE=InnoDB;

CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    cc INT NULL,
    id_rol_fk INT NOT NULL,
    correo VARCHAR(255) UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    horas_mes INT,
    avatar_path VARCHAR(255) NULL,
    avatar_mime VARCHAR(100) NULL,
    avatar_size INT NULL,
    avatar_uploaded_at DATETIME NULL,
    fch_registro DATETIME,
    fch_ult_act DATETIME,
    id_vinculacion_fk INT NULL,
    PRIMARY KEY (id_usuario),
    UNIQUE KEY uniq_cc (cc),
    INDEX idx_usuario_id_rol_fk (id_rol_fk),
    INDEX idx_usuario_id_vinculacion_fk (id_vinculacion_fk),
    CONSTRAINT fk_usuario_rol
        FOREIGN KEY (id_rol_fk)
        REFERENCES rol(id_rol)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_usuario_vinculacion
        FOREIGN KEY (id_vinculacion_fk)
        REFERENCES vinculacion(id_vinculacion)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE notificacion (
    id_noti INT NOT NULL AUTO_INCREMENT,
    cc_usuario_fk INT NULL,
    fch_noti DATE NOT NULL,
    hora_noti TIME NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    estado TINYINT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_noti),
    INDEX idx_notificacion_cc_usuario_fk (cc_usuario_fk),
    CONSTRAINT fk_notificacion_usuario_cc
        FOREIGN KEY (cc_usuario_fk)
        REFERENCES usuario(cc)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE sede (
    cod_sede INT NOT NULL AUTO_INCREMENT,
    nom_sede VARCHAR(255),
    municipio VARCHAR(120) NULL,
    fch_registro DATETIME,
    fch_ult_act DATETIME,
    PRIMARY KEY (cod_sede),
    INDEX idx_sede_cod_sede (cod_sede)
) ENGINE=InnoDB;

CREATE TABLE ambiente (
    cod_amb INT NOT NULL AUTO_INCREMENT,
    denominacion VARCHAR(255),
    cod_sede_fk INT NOT NULL,
    PRIMARY KEY (cod_amb),
    INDEX idx_ambiente_cod_sede_fk (cod_sede_fk),
    CONSTRAINT fk_ambiente_sede
        FOREIGN KEY (cod_sede_fk)
        REFERENCES sede(cod_sede)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE bloque (
    id_bloc INT NOT NULL AUTO_INCREMENT,
    hora_inicio TIME,
    hora_fin TIME,
    jornada VARCHAR(20),
    descripcion VARCHAR(20),
    PRIMARY KEY (id_bloc),
    INDEX idx_bloque_id_bloc (id_bloc)
) ENGINE=InnoDB;

CREATE TABLE hora (
    id_hora INT NOT NULL AUTO_INCREMENT,
    hora_inicio TIME,
    hora_fin TIME,
    id_fich_fk INT NOT NULL,
    id_horario_fk INT NOT NULL,
    id_usuario_fk INT,
    cod_sede_fk INT,
    cod_amb_fk INT,
    fch_registro DATETIME,
    fch_ult_act DATETIME,
    id_bloc_fk INT,
    PRIMARY KEY (id_hora),
    INDEX idx_hora_id_fich_fk (id_fich_fk),
    INDEX idx_hora_id_horario_fk (id_horario_fk),
    INDEX idx_hora_id_usuario_fk (id_usuario_fk),
    INDEX idx_hora_cod_sede_fk (cod_sede_fk),
    INDEX idx_hora_cod_amb_fk (cod_amb_fk),
    INDEX idx_hora_id_bloc_fk (id_bloc_fk),
    CONSTRAINT fk_hora_bloque
        FOREIGN KEY (id_bloc_fk)
        REFERENCES bloque(id_bloc)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_hora_ficha
        FOREIGN KEY (id_fich_fk)
        REFERENCES ficha(id_fich)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_hora_horario
        FOREIGN KEY (id_horario_fk)
        REFERENCES horario(id_horario)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_hora_usuario
        FOREIGN KEY (id_usuario_fk)
        REFERENCES usuario(id_usuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_hora_sede
        FOREIGN KEY (cod_sede_fk)
        REFERENCES sede(cod_sede)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    CONSTRAINT fk_hora_ambiente
        FOREIGN KEY (cod_amb_fk)
        REFERENCES ambiente(cod_amb)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB;

DELIMITER $$

CREATE TRIGGER tr_programa_update_programa
BEFORE UPDATE ON programa
FOR EACH ROW
BEGIN
    SET NEW.fhc_utl_act_prg = NOW();
END$$

CREATE TRIGGER tr_competencia_update_programa
BEFORE UPDATE ON competencia
FOR EACH ROW
BEGIN
    UPDATE programa
    SET fhc_utl_act_prg = NOW()
    WHERE cod_prog = NEW.id_prog_fk;
END$$

CREATE TRIGGER tr_resultado_update_programa
BEFORE UPDATE ON resultado
FOR EACH ROW
BEGIN
    UPDATE programa
    SET fhc_utl_act_prg = NOW()
    WHERE cod_prog = (
        SELECT c.id_prog_fk
        FROM competencia c
        WHERE c.id_comp = NEW.id_comp_fk
        LIMIT 1
    )
      AND NEW.id_comp_fk IS NOT NULL;
END$$

DELIMITER ;

INSERT INTO horario (dia) VALUES
('Lunes'),
('Martes'),
('Miercoles'),
('Jueves'),
('Viernes'),
('Sabado');

INSERT INTO bloque (hora_inicio, hora_fin, descripcion) VALUES
('07:00:00', '11:00:00', '4 HORAS manana'),
('06:00:00', '12:00:00', '6 HORAS manana'),
('12:00:00', '18:00:00', '6 HORAS tarde'),
('12:00:00', '16:00:00', '4 HORAS tarde'),
('13:00:00', '17:00:00', '4 HORAS tarde'),
('16:00:00', '22:00:00', '6 HORAS noche'),
('18:00:00', '22:00:00', '4 HORAS noche');

INSERT INTO rol (id_rol, nombre_rol) VALUES
(1, 'admin'),
(2, 'contrato'),
(3, 'planta');

INSERT INTO usuario (cc, id_rol_fk, correo, contrasena, nombre, fch_registro)
VALUES (10000, 1, 'zeamartinezjohan@gmail.com', 'admin', 'Johan Martinez', NOW());
